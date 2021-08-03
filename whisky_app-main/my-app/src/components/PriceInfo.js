import React, { Component } from "react";
import "../scss/price-info.scss";

class PriceInfo extends Component {
  render() {
    let items = [];
    let data = this.props.price_table;
    let count = 0;

    if (Object.keys(data).length > 0) {
      for (let item in data) {
        items.push(
          <ShopItem
            shop={data[item]["Shop"]}
            address={data[item]["Address"]}
            price={data[item]["Price"]}
            key={count}
          ></ShopItem>
        );
        count++;
      }
      return (
        <div className="price-info">
          <div className="price-info__distribution">
            <h2>Price Distribution</h2>
            <figure
              className="placeholder-center placeholder-center--w-100 placeholder-center--wordcloud"
              data-aos="fade-left"
            >
              <img
                className="placeholder-center__item"
                src={"data:image/png;base64," + this.props.img}
              ></img>
            </figure>
          </div>
          <div className="price-info__shops-wrap">
            <h2>Shops</h2>
            <div className="price-info__shops">{items}</div>
          </div>
        </div>
      );
    } else {
      return (
        <div className="price-info">
          <div className="price-info__shops-wrap">
            <h2>Shops</h2>
            <p>Not available in Hong Kong</p>
          </div>
        </div>
      );
    }
  }
}

function ShopItem(props) {
  let address = props.address;
  let htmlMatch = address.match("https://");
  let chineseMatch = address.search("號");
  if (htmlMatch) {
    return (
      <div className="price-info__shop-item" data-aos="fade-up">
        <div className="price-info__shop-item-info">
          <h3 className="price-info__shop-item-shop">{props.shop}</h3>
          <p className="price-info__shop-item-address">
            <a href={address} target="_blank">
              {address}
            </a>
          </p>
        </div>
        <p className="price-info__shop-item-price">${props.price}</p>
      </div>
    );
  } else if (chineseMatch != -1) {
    return (
      <div className="price-info__shop-item" data-aos="fade-up">
        <div className="price-info__shop-item-info">
          <h3 className="price-info__shop-item-shop">{props.shop}</h3>
          <p className="price-info__shop-item-address">
            <a
              href={
                "https://www.google.com.hk/maps/place/" +
                address.slice(0, chineseMatch + 1)
              }
              target="_blank"
            >
              {address}
            </a>
          </p>
        </div>
        <p className="price-info__shop-item-price">${props.price}</p>
      </div>
    );
  } else {
    return (
      <div className="price-info__shop-item" data-aos="fade-up">
        <div className="price-info__shop-item-info">
          <h3 className="price-info__shop-item-shop">{props.shop}</h3>
          <p className="price-info__shop-item-address">{props.address}</p>
        </div>
        <p className="price-info__shop-item-price">${props.price}</p>
      </div>
    );
  }
}

export default PriceInfo;
