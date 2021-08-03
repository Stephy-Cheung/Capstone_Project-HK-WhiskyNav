import React, { Component } from "react";
import ImageUpload from "../components/imageload";
import axios from "axios";
import Bottle from "../components/Bottle";
import FilterSliderList from "../components/FilterSlider";
import "../scss/flex.scss";
import Aos from "aos";
import { animateScroll as scroll } from "react-scroll";
class Home extends Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedFile: null,
      fileURL: null,
      search_whisky_data: null,
      falvour_recommend_list: null,
      activated_falvour_search: false,
      loading_image: false,
    };
  }

  fileSelectedHandler = (e) => {
    const fd = new FormData();
    fd.append("image", e.target.files[0], e.target.files[0].name);
    this.setState({
      loading_image: true,
      selectedFile: e.target.files[0],
      fileURL: URL.createObjectURL(e.target.files[0]),
    });
    axios.post("http://127.0.0.1:5000/searchImage", fd).then((res) => {
      // console.log(res["data"]["whiskies"]);
      this.setState({
        loading_image: false,
        search_whisky_data: res["data"]["whiskies"],
      });
      if (res["data"]["whiskies"]) {
        let recommend = document.getElementById("flavour-recommend-1");

        if (this.state.search_whisky_data != "N/A") {
          if (window.scrollY + window.innerHeight < recommend.offsetTop + 100) {
            scroll.scrollTo(recommend.offsetTop - 100);
          }
        } else {
          if (window.scrollY + window.innerHeight < recommend.offsetTop + 50) {
            scroll.scrollTo(recommend.offsetTop - window.innerHeight + 50);
          }
        }
      }
    });
  };

  // fileUploadHandler = () => {
  //   if (this.state.selectedFile != null) {
  //     const fd = new FormData();
  //     fd.append("image", this.state.selectedFile, this.state.selectedFile.name);
  //     axios.post("http://127.0.0.1:5000/searchImage", fd).then((res) => {
  //       this.setState({
  //         whisky_index_predicted: res["data"]["index"],
  //         whisky_name_predicted: res["data"]["name"],
  //         whisky_year_predicted: res["data"]["year"],
  //       });
  //     });
  //   }
  // };

  handleUpdate = (data) => {
    this.setState({
      falvour_recommend_list: data,
      activated_falvour_search: true,
    });
    if (data) {
      let recommend = document.getElementById("flavour-recommend-2");

      if (window.scrollY + window.innerHeight < recommend.offsetTop + 100) {
        scroll.scrollTo(recommend.offsetTop - 100);
      }
      Aos.refresh();
    }
  };

  render() {
    return (
      <div className="home">
        <h1>HK WhiskyNav</h1>
        <p>
          HK WhiskyNav uses Machine Learning to provide whisky identification,
          selling info consolidation, flavour analysis and recommendation
          services in one go. User can upload a photo or image of a whisky
          bottle, the app then applies Deep Learning technology to distinguish
          100 different popular whiskies found in HK and identify the correct
          brand and year. After identification, the app then consolidates the
          information, including price range, name and address of all available
          shops in HK. Furthermore, through Machine Learning, the app can
          analyse the flavour profile of the whisky and display an
          easy-to-understand flavour description to the user. Through the
          anaylsis of the flavour profile, the app can also accurately recommend
          similar whisky, or completely different whisky for user to explore.
        </p>
        <div className="section">
          <h2>Search by Image</h2>
          <input
            className="image-search-upload"
            type="file"
            onChange={this.fileSelectedHandler}
          />
          {/* <button onClick={this.fileUploadHandler}>Upload</button> */}
          <Bottle
            url={this.state.fileURL}
            loading={this.state.loading_image}
          ></Bottle>
          <Comfirm_predict data={this.state.search_whisky_data} />
        </div>

        <div className="section">
          <h2>Search by Flavour Profile</h2>
          <FilterSliderList handleUpdate={this.handleUpdate}></FilterSliderList>
          <FalvourWhiskies
            falvour_recommend_list={this.state.falvour_recommend_list}
            activated_falvour_search={this.state.activated_falvour_search}
          ></FalvourWhiskies>
        </div>
      </div>
    );
  }
}

class Comfirm_predict extends Component {
  render() {
    if (this.props.data) {
      let whiskies = this.props.data;
      if (whiskies != "N/A") {
        let index = Object.keys(whiskies)[0];

        return (
          <div className="flavour-recommend" id="flavour-recommend-1">
            <h2>Is this what you are finding?</h2>
            <div className="flavour-recommend__list">
              <FlavourWhiskyItem
                data={whiskies[index]}
                index={index}
                key={index}
              />
            </div>
          </div>
        );
      } else {
        return (
          <div className="flavour-recommend" id="flavour-recommend-1">
            <p className="error">
              Your image seems not to be whisky. Please try another image
            </p>
          </div>
        );
      }
    } else {
      return null;
    }
  }
}

class FalvourWhiskies extends Component {
  constructor(props) {
    super(props);
    Aos.init({
      duration: 600,
      once: true,
      offset: 50,
    });
  }
  componentDidMount() {}
  render() {
    if (this.props.activated_falvour_search) {
      if (this.props.falvour_recommend_list) {
        let whiskies = this.props.falvour_recommend_list;

        let items = [];

        for (let item in whiskies) {
          items.push(
            <FlavourWhiskyItem data={whiskies[item]} index={item} key={item} />
          );
        }

        return (
          <div className="flavour-recommend" id="flavour-recommend-2">
            <h2>Search Result</h2>
            <div className="flavour-recommend__list">{items}</div>
          </div>
        );
      } else {
        return (
          <div className="flavour-recommend">
            <h2>Search Result</h2>
            <div className="flavour-recommend__list">
              <p>No result</p>
            </div>
          </div>
        );
      }
    } else {
      return null;
    }
  }
}

function FlavourWhiskyItem(props) {
  let data = props.data;
  let index = props.index;

  return (
    <div className="flavour-recommend__item" data-aos="fade-up">
      <a className="flex" href={"/whisky/" + index}>
        <div className="flex__media">
          <figure className="placeholder-center placeholder-center--1-to-1">
            <img
              className="placeholder-center__item"
              src={"/images/bottles/" + index + ".jpg"}
              alt=""
            ></img>
          </figure>
        </div>
        <div className="flex__body">
          <p className="flex__title">{data["Name"] + " " + data["Year"]}</p>
        </div>
      </a>
    </div>
  );
}

export default Home;
