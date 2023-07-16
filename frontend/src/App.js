import React, { useState } from "react";
import "./App.css";
import jQuery from "jquery";

function App() {
  const [site, setSite] = useState("");
  const [webhook, setWebhook] = useState("");
  const [submitStatus, setSubmitStatus] = useState("");
  const [state, setState] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();

    const data = {
      site: site,
      webhook: webhook,
    };

    function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie !== "") {
        var cookies = document.cookie.split(";");
        for (var i = 0; i < cookies.length; i++) {
          var cookie = jQuery.trim(cookies[i]);
          if (cookie.substring(0, name.length + 1) === name + "=") {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
          }
        }
      }
      return cookieValue;
    }

    const csrfToken = getCookie("csrftoken");

    fetch("/api/data", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
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
        } else if (data["status"] === "error") {
          setSubmitStatus("An unknown error occurred.");
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
