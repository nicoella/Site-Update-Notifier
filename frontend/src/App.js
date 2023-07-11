import "./App.css";

function App() {
  return (
    <div className="App">
      <h1>Site Update Notifier</h1>
      <p>
        This is a site update tracking bot. Please enter the site you would like
        to track updates on and a link to a webhook you would like the updates
        to be posted to.
      </p>
      <form>
        <div class="input">
          <label for="input1">Site to Track: </label>
          <input type="text" id="input1" name="input1"></input>
        </div>

        <div class="input">
          <label for="input2">Webhook Link: </label>
          <input type="text" id="input2" name="input2"></input>
        </div>

        <button type="submit">Submit</button>
      </form>
    </div>
  );
}

export default App;
