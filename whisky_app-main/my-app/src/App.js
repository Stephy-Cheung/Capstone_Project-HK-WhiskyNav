import logo from "./logo.svg";
import "bootstrap/dist/css/bootstrap.min.css";
import "./scss/inner-generic.scss";
import Home from "./pages/home";
import Whisky from "./pages/whisky";

import {
  BrowserRouter,
  Route,
  Link,
  match,
  Switch,
  Redirect,
} from "react-router-dom";

function App() {
  let dt = new Date();
  return (
    <div className="inner-container">
      <div className="container">
        <main>
          <BrowserRouter>
            <div className="App">
              <Switch>
                <Route exact path="/" component={Home} />
                <Route path="/whisky/:id" component={Whisky} />
              </Switch>
            </div>
          </BrowserRouter>
        </main>
        <footer>
          <p className="copyright">
            Copyright © {dt.getFullYear()} HK WhiskyNav. All Rights Reserved.
          </p>
        </footer>
      </div>
    </div>
  );
}

export default App;
