import React, { useState } from "react";
import "./App.css";

function App() {
  const [site, setSite] = useState("");
  const [webhook, setWebhook] = useState("");
  const [submitStatus, setSubmitStatus] = useState("");
  const [state, setState] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault(); // Prevent the default form submission behavior

    // Create a data object with the form input values
    const data = {
      site: site,
      webhook: webhook,
    };

    // Send the form data to the backend using fetch
    fetch("/api/data", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        if (data["status"] === "success") {
          setSubmitStatus(
            "Site successfully tracked. A notification was sent to your webhook."
          );
          setState("valid");
          setSite("");
          setWebhook("");
        } else if (data["status"] === "bad insert") {
          setSubmitStatus("Error inserting into the database.");
          setState("error");
        } else if (data["status"] === "bad webhook") {
          setSubmitStatus(
            "Error setting the webhook. Please double-check the link."
          );
          setState("error");
        }
      })
      .catch((error) => {
        console.error(error);
      });
  };

  return (
    <div className="App">
      <h1>Site Update Notifier</h1>
      <p>
        This is a site update tracking bot. Please enter the site you would like
        to track updates on and a link to a webhook you would like the updates
        to be posted to.
      </p>
      <form onSubmit={handleSubmit} method="POST">
        <div className="input">
          <label htmlFor="input1">Site to Track: </label>
          <input
            type="text"
            id="input1"
            name="site"
            value={site}
            onChange={(e) => setSite(e.target.value)}
          ></input>
        </div>

        <div className="input">
          <label htmlFor="input2">Webhook Link: </label>
          <input
            type="text"
            id="input2"
            name="webhook"
            value={webhook}
            onChange={(e) => setWebhook(e.target.value)}
          />
        </div>
        <button type="submit">Submit</button>
      </form>
      <div className={state}>{submitStatus}</div>
    </div>
  );
}

export default App;
