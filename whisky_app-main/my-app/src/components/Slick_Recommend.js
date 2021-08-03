import React, { Component } from "react";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import "../scss/slick.scss";
import "../scss/placeholder.scss";
import "../scss/recommend.scss";

class Slick_Recommend extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    let settings = {
      autoplay: true,
      autoplaySpeed: 8000,
      dots: true,
      infinite: true,
      speed: 600,
      slidesToShow: 3,
      slidesToScroll: 3,
      responsive: [
        {
          breakpoint: 992,
          settings: {
            slidesToShow: 2,
            slidesToScroll: 2,
            arrows: false,
          },
        },
        {
          breakpoint: 576,
          settings: {
            slidesToShow: 1,
            slidesToScroll: 1,
            arrows: false,
          },
        },
      ],
    };

    let items = [];

    let df = this.props.data;

    for (let item in df) {
      items.push(
        <Slick_item
          index={item}
          name={df[item]["Name"]}
          year={df[item]["Year"]}
          key={item}
        ></Slick_item>
      );
    }

    if (Object.keys(df).length < 3) {
      if (Object.keys(df).length < 2) {
        settings["slidesToShow"] = 1;
        settings["slidesToScroll"] = 1;
        settings["responsive"] = [];
      } else {
        settings["slidesToShow"] = 2;
        settings["slidesToScroll"] = 2;
      }
    }

    return (
      <div className="slider-wrap" data-aos="zoom-in-up" data-aos-delay="200">
        <Slider {...settings}>{items}</Slider>
      </div>
    );
  }
}

class Slick_item extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    if (this.props.index) {
      return (
        <div className="slider__item">
          <a className="recommend" href={"/whisky/" + this.props.index}>
            <div className="recommend__media">
              <div className="placeholder-center placeholder-center--1-to-1">
                <img
                  className="placeholder-center__item"
                  src={"/images/bottles/" + this.props.index + ".jpg"}
                ></img>
              </div>
            </div>
            <div className="recommend__body">
              <p className="recommend__title">
                {this.props.name + " " + this.props.year}
              </p>
            </div>
          </a>
        </div>
      );
    } else {
      return (
        <div className="slider__item">
          <a className="recommend">
            <div className="recommend__media">
              <div className="placeholder-center placeholder-center--1-to-1"></div>
            </div>
          </a>
        </div>
      );
    }
  }
}

export default Slick_Recommend;
