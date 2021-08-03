import React, { Component } from "react";

class WordCloud extends Component {
  render() {
    if (this.props.image) {
      return (
        <div className="wordcloud">
          <h2>Key Words from Reviews</h2>
          <figure
            className="placeholder-center placeholder-center--w-100 placeholder-center--wordcloud"
            data-aos="fade-right"
          >
            <img
              className="placeholder-center__item"
              src={`data:image/png;base64,${this.props.image}`}
            ></img>
          </figure>
        </div>
      );
    } else {
      return null;
    }
  }
}

export default WordCloud;
