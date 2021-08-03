import React, { Component } from "react";
import Bottle from "../components/Bottle";
import axios from "axios";
import Slick_Recommend from "../components/Slick_Recommend";
import WordCloud from "../components/WordCloud";
import PriceInfo from "../components/PriceInfo";
import "../scss/placeholder.scss";
import "../scss/button.scss";
import "../scss/whisky.scss";
import AOS from "aos";
import "aos/dist/aos.css";

class Whisky extends Component {
  state = {
    id: this.props.match.params.id,
    data: null,
  };

  componentDidMount() {
    if (this.state.data == null) {
      axios.get("http://127.0.0.1:5000/whisky/" + this.state.id).then((res) => {
        this.setState({
          data: res["data"],
        });
        AOS.init({
          duration: 600,
          once: true,
        });
      });
    }
  }

  render() {
    const url = "/images/bottles/" + this.state.id + ".jpg";

    if (this.state.data) {
      return (
        <div className="whisky">
          <div className="btn-group btn-group--reverse">
            <a className="btn btn--black btn--back" href="/">
              Back to Home Page
            </a>
          </div>
          <div className="section">
            <h1 className="whisky__title">
              <span className="whisky__title-bottle">
                {this.state.data["info"]["Name"] +
                  " " +
                  this.state.data["info"]["Year"] +
                  " "}
              </span>
              <span className="whisky__title-vol">
                {this.state.data["volume"]
                  ? "(" + this.state.data["volume"] + ")"
                  : null}
              </span>
            </h1>
            <Bottle url={url}></Bottle>
          </div>
          <div className="section">
            <WordCloud image={this.state.data["wordcloud"]} />
          </div>
          <div className="section">
            <PriceInfo
              img={this.state.data["price_img"]}
              price_table={this.state.data["price_table"]}
            ></PriceInfo>
          </div>
          <div className="section">
            <Slick recommend={this.state.data["recommend"]}></Slick>
          </div>
          <div className="section">
            <Slick
              opposite_recommend={this.state.data["opposite_recommend"]}
            ></Slick>
          </div>
        </div>
      );
    } else {
      return null;
    }
  }
}

function Slick(props) {
  if (props.recommend || props.opposite_recommend) {
    let similar = null;
    let opposite = null;
    if (props.recommend) {
      similar = (
        <div>
          <h2>Recommendation</h2>
          <Slick_Recommend data={props.recommend}></Slick_Recommend>
        </div>
      );
    } else {
      similar = (
        <div>
          <h2>Recommendation</h2>
          <p>No fiited whiskies available in Hong Kong</p>
        </div>
      );
    }
    if (props.opposite_recommend) {
      similar = (
        <div>
          <h2>Recommendation (Opposite)</h2>
          <Slick_Recommend data={props.opposite_recommend}></Slick_Recommend>
        </div>
      );
    }

    return (
      <div>
        {similar}
        {opposite}
      </div>
    );
  } else {
    return null;
  }
}

export default Whisky;
