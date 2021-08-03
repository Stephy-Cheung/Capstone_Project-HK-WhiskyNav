import { refresh } from "aos";
import React, { Component } from "react";
import "../scss/loading.scss";
import "../scss/bottle.scss";

class Bottle extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    if (this.props.url != null) {
      return (
        <div className={this.props.loading ? "bottle loading" : "bottle"}>
          <figure className="placeholder-center placeholder-center--1-to-1">
            <img
              className="placeholder-center__item"
              src={this.props.url}
              alt="whisky bottle"
            ></img>
          </figure>
          <Loading loading={this.props.loading}></Loading>
        </div>
      );
    } else {
      return null;
    }
  }
}

function Loading(props) {
  if (props.loading) {
    return (
      <div class="bottle__loading lds-roller">
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
        <div></div>
      </div>
    );
  } else {
    return null;
  }
}

export default Bottle;
