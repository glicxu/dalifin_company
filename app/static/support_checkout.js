const paymentForm = document.querySelector("#support-payment-form");
const submitButton = document.querySelector("#submit-payment");
const amountInput = document.querySelector("#amount-input");
const messageEl = document.querySelector("#payment-message");
const spinner = document.querySelector("#payment-spinner");
const quickAmountButtons = Array.from(document.querySelectorAll(".quick-amount"));
const resetButton = document.querySelector("#reset-payment");
const statusOverlay = document.querySelector("#payment-status-overlay");
const statusTitle = document.querySelector("#payment-status-title");
const statusMessage = document.querySelector("#payment-status-message");
const statusReference = document.querySelector("#payment-status-reference");
const modalClose = document.querySelector("#payment-modal-close");
const modalDismiss = document.querySelector("#payment-modal-dismiss");

let stripe;
let elements;
let paymentElement;
let currentClientSecret;
let refreshTimeoutId;
let lastFocusedElement;

const REFRESH_DELAY_MS = 400;

const parseDollarsToCents = (value) => {
  const numberValue = Number.parseFloat(String(value));
  if (!Number.isFinite(numberValue)) {
    return Number.NaN;
  }
  return Math.round(numberValue * 100);
};

const formatCentsToDollars = (cents) => {
  const dollars = cents / 100;
  return Number.isInteger(dollars) ? String(dollars) : dollars.toFixed(2);
};

const formatCentsLabel = (cents) => {
  const dollars = cents / 100;
  return cents % 100 === 0 ? String(dollars) : dollars.toFixed(2);
};

const setStatus = (message, variant = "info") => {
  messageEl.textContent = message || "";
  messageEl.classList.remove("success", "error", "info");
  if (message) {
    messageEl.classList.add(variant);
  }
};

const toggleLoading = (isLoading) => {
  submitButton.disabled = isLoading;
  spinner.hidden = !isLoading;
};

const syncQuickAmountSelection = () => {
  const cents = parseDollarsToCents(amountInput.value);
  let matched = false;

  quickAmountButtons.forEach((button) => {
    if (button.dataset.amount === "custom") {
      return;
    }
    const presetValue = Number.parseInt(button.dataset.amount, 10);
    const isSelected = Number.isFinite(cents) && cents === presetValue;
    matched = matched || isSelected;
    button.setAttribute("aria-pressed", String(isSelected));
    button.classList.toggle("is-selected", isSelected);
  });

  const customButton = quickAmountButtons.find((button) => button.dataset.amount === "custom");
  if (customButton) {
    customButton.setAttribute("aria-pressed", String(!matched));
    customButton.classList.toggle("is-selected", !matched);
  }
};

const updateSupportButton = () => {
  const cents = parseDollarsToCents(amountInput.value);
  if (Number.isFinite(cents) && cents >= 100) {
    submitButton.textContent = `Support Dalifin - $${formatCentsLabel(cents)}`;
  } else {
    submitButton.textContent = "Support Dalifin";
  }
};

const openStatusModal = ({ title, detail, reference, variant = "info" }) => {
  statusTitle.textContent = title;
  statusMessage.textContent = detail || "";
  statusReference.textContent = reference || "";
  statusReference.dataset.hidden = reference ? "false" : "true";
  statusOverlay.classList.remove("success", "error", "info");
  statusOverlay.classList.add(variant);
  statusOverlay.dataset.hidden = "false";
  statusOverlay.setAttribute("aria-hidden", "false");
  lastFocusedElement = document.activeElement;
  document.body.style.setProperty("overflow", "hidden");
  modalDismiss.focus();
};

const closeStatusModal = () => {
  statusOverlay.dataset.hidden = "true";
  statusOverlay.setAttribute("aria-hidden", "true");
  statusReference.dataset.hidden = "true";
  document.body.style.removeProperty("overflow");
  if (lastFocusedElement && typeof lastFocusedElement.focus === "function") {
    lastFocusedElement.focus();
  }
};

const createPaymentIntent = async (amount) => {
  const response = await fetch("/support/api/create-payment-intent", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      amount,
      currency: "usd",
      metadata: {
        amount_source: "dalifin_support_page",
      },
    }),
  });
  return response.json();
};

const resetFormState = () => {
  resetButton.hidden = false;
  submitButton.disabled = true;
  paymentElement?.destroy();
  paymentElement = undefined;
};

const setupPaymentElement = async () => {
  currentClientSecret = undefined;
  submitButton.disabled = true;
  paymentElement?.destroy();
  paymentElement = undefined;

  const amount = parseDollarsToCents(amountInput.value);
  if (!Number.isFinite(amount) || amount < 100) {
    setStatus("Enter a valid amount. Minimum payment is $1.", "error");
    return;
  }

  setStatus("Preparing secure card form...", "info");

  try {
    toggleLoading(true);
    const { clientSecret, error } = await createPaymentIntent(amount);
    if (error || !clientSecret) {
      setStatus(error || "Unable to initialize the payment form.", "error");
      return;
    }

    currentClientSecret = clientSecret;
    elements = stripe.elements({
      clientSecret,
      appearance: {
        theme: "night",
        labels: "floating",
      },
    });
    paymentElement = elements.create("payment");
    paymentElement.mount("#payment-element");
    submitButton.disabled = false;
    setStatus("Card form ready. Complete payment when ready.", "info");
  } catch (error) {
    console.error("Failed to set up Stripe Elements:", error);
    setStatus("Unable to load the payment form.", "error");
  } finally {
    toggleLoading(false);
  }
};

const schedulePaymentElementRefresh = () => {
  currentClientSecret = undefined;
  submitButton.disabled = true;
  if (refreshTimeoutId) {
    clearTimeout(refreshTimeoutId);
  }
  refreshTimeoutId = setTimeout(setupPaymentElement, REFRESH_DELAY_MS);
};

const initializeStripe = async () => {
  try {
    const config = await fetch("/support/api/config").then((res) => res.json());
    if (!config.publishableKey) {
      setStatus(config.error || "Stripe publishable key is unavailable.", "error");
      submitButton.disabled = true;
      return;
    }
    stripe = Stripe(config.publishableKey);
    await setupPaymentElement();
  } catch (error) {
    console.error("Failed to initialize Stripe:", error);
    setStatus("Unable to load payment configuration.", "error");
  }
};

paymentForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  if (!paymentElement || !currentClientSecret) {
    setStatus("Payment form is not ready yet.", "error");
    return;
  }

  const amount = parseDollarsToCents(amountInput.value);
  if (!Number.isFinite(amount) || amount < 100) {
    setStatus("Enter a valid amount. Minimum payment is $1.", "error");
    return;
  }

  toggleLoading(true);

  try {
    const { error: elementError } = await elements.submit();
    if (elementError) {
      setStatus(elementError.message, "error");
      openStatusModal({
        title: "Payment failed",
        detail: elementError.message,
        variant: "error",
      });
      return;
    }

    const { error, paymentIntent } = await stripe.confirmPayment({
      elements,
      clientSecret: currentClientSecret,
      confirmParams: {
        return_url: window.location.href,
      },
      redirect: "if_required",
    });

    if (error) {
      setStatus(error.message, "error");
      openStatusModal({
        title: "Payment failed",
        detail: error.message,
        reference: error.payment_intent?.id ? `Payment ID: ${error.payment_intent.id}` : "",
        variant: "error",
      });
      return;
    }

    setStatus("Payment completed successfully.", "success");
    openStatusModal({
      title: "Payment received",
      detail: "Thank you. Your card was charged successfully.",
      reference: paymentIntent?.id ? `Payment ID: ${paymentIntent.id}` : "",
      variant: "success",
    });
    resetFormState();
  } catch (error) {
    console.error("Stripe confirmation failed:", error);
    setStatus("Payment request failed.", "error");
    openStatusModal({
      title: "Payment request failed",
      detail: "Unexpected error while contacting Stripe.",
      variant: "error",
    });
  } finally {
    toggleLoading(false);
  }
});

quickAmountButtons.forEach((button) => {
  button.addEventListener("click", () => {
    if (button.dataset.amount === "custom") {
      amountInput.focus();
      amountInput.select?.();
      syncQuickAmountSelection();
      updateSupportButton();
      return;
    }

    const cents = Number.parseInt(button.dataset.amount, 10);
    if (!Number.isFinite(cents)) {
      return;
    }
    amountInput.value = formatCentsToDollars(cents);
    syncQuickAmountSelection();
    updateSupportButton();
    schedulePaymentElementRefresh();
  });
});

amountInput.addEventListener("input", () => {
  syncQuickAmountSelection();
  updateSupportButton();
  schedulePaymentElementRefresh();
});

resetButton.addEventListener("click", () => {
  amountInput.value = "25";
  resetButton.hidden = true;
  syncQuickAmountSelection();
  updateSupportButton();
  closeStatusModal();
  schedulePaymentElementRefresh();
});

modalClose.addEventListener("click", closeStatusModal);
modalDismiss.addEventListener("click", closeStatusModal);
statusOverlay.addEventListener("click", (event) => {
  if (event.target === statusOverlay) {
    closeStatusModal();
  }
});
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && statusOverlay.dataset.hidden === "false") {
    closeStatusModal();
  }
});

syncQuickAmountSelection();
updateSupportButton();
initializeStripe();
