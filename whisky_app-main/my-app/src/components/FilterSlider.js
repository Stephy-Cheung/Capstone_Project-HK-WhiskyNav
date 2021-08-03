import React, { Component } from "react";
import Slider from "@material-ui/core/Slider";
import Accordion from "react-bootstrap/Accordion";
import Button from "react-bootstrap/Button";
import axios from "axios";
import "../scss/filterlist.scss";
import "../scss/accordion.scss";

class FilterSliderList extends Component {
  constructor(props) {
    super(props);
    this.state = {
      Body: 2,
      Sweetness: 2,
      Smoky: 2,
      Medicinal: 2,
      Tobacco: 2,
      Honey: 2,
      Spicy: 2,
      Winey: 2,
      Nutty: 2,
      Malty: 2,
      Fruity: 2,
      Floral: 2,
      reverse: false,
    };

    this.ChildChange = this.ChildChange.bind(this);
    this.handleClick = this.handleClick.bind(this);
    this.handleReset = this.handleReset.bind(this);
  }

  ChildChange(name) {
    return (e, val) => {
      this.setState({
        [name]: val,
      });
    };
  }

  handleClick() {
    axios
      .post("http://127.0.0.1:5000/searchFlavours", { flavours: this.state })
      .then((res) => {
        this.props.handleUpdate(res["data"]["recommend"]);
      });
  }

  handleReset() {
    this.setState({
      Body: 2,
      Sweetness: 2,
      Smoky: 2,
      Medicinal: 2,
      Tobacco: 2,
      Honey: 2,
      Spicy: 2,
      Winey: 2,
      Nutty: 2,
      Malty: 2,
      Fruity: 2,
      Floral: 2,
      reverse: false,
    });
  }

  render() {
    let flavours = [
      "Body",
      "Sweetness",
      "Smoky",
      "Medicinal",
      "Tobacco",
      "Honey",
      "Spicy",
      "Winey",
      "Nutty",
      "Malty",
      "Fruity",
      "Floral",
    ];
    let top4 = ["Smoky", "Honey", "Winey", "Fruity"];
    let items = [];
    let specials = [];
    for (let item in flavours) {
      if (top4.includes(flavours[item])) {
        specials.push(
          <FilterSlider
            flavour={flavours[item]}
            handleChange={this.ChildChange(flavours[item])}
            key={flavours[item]}
            value={this.state[flavours[item]]}
          ></FilterSlider>
        );
      } else {
        items.push(
          <FilterSlider
            flavour={flavours[item]}
            handleChange={this.ChildChange(flavours[item])}
            key={flavours[item]}
            value={this.state[flavours[item]]}
          ></FilterSlider>
        );
      }
    }

    return (
      <div className="filter-list-wrap">
        <div className="filter-list">{specials}</div>
        <Accordion>
          <Accordion.Collapse eventKey="0" className="accordion__collapse">
            <div className="filter-list">{items}</div>
          </Accordion.Collapse>
          {/* <div className="filter-list">{items.slice(0, 4)}</div> */}
          <div className="accordion__toggle-wrap">
            <Accordion.Toggle
              className="accordion__toggle"
              eventKey="0"
              as={Button}
              variant="link"
            >
              <span className="accordion__toggle-expand">More flavours</span>
              <span className="accordion__toggle-collapse">Less flavours</span>
            </Accordion.Toggle>
          </div>
        </Accordion>
        <div className="filter-btns">
          <Button variant="dark" onClick={this.handleClick}>
            Search
          </Button>
          <Button variant="light" onClick={this.handleReset}>
            Reset
          </Button>
        </div>
      </div>
    );
  }
}

class FilterSlider extends Component {
  constructor(props) {
    super(props);
    this.state = {
      flavour: this.props.flavour,
    };
  }

  render() {
    return (
      <div className="filter-list__item">
        <p>{this.state.flavour}</p>
        <Slider
          value={this.props.value}
          // getAriaValueText={valuetext}
          aria-labelledby="discrete-slider"
          valueLabelDisplay="auto"
          step={0.5}
          marks
          min={0}
          max={4}
          onChangeCommitted={this.props.handleChange}
        />
      </div>
    );
  }
}

export default FilterSliderList;
