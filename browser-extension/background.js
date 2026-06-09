chrome.runtime.onMessage.addListener(async (message, sender, sendResponse) => {
  if (message.type !== "fen") {
    return;
  }

  try {
    const response = await fetch("http://127.0.0.1:5000/fen", {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        fen: message.fen,
      }),
    });

    const data = await response.json();

    sendResponse(data);
  } catch (error) {
    sendResponse({
      error: error.toString(),
    });
  }

  return true;
});
