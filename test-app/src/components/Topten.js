import React, { Component } from "react";
import axios from "axios";

class Topten extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: []
    };
  }
  componentDidMount() {
    this.getData();
  }

  getData = () => {
    axios.get("http://d3a5e2b4f35e:80/api/top_10").then(response => {
      console.log(response);
      this.setState({ data: response.top_10 });
    });
    fetch("http://scraper-api:80/api/top_10").then(data => {
      console.log(data);
      this.setState({ data: data.top_10 });
    });
  };
  render() {
    const top_10 = this.state.data.map((player, index) => {
      return <li key={index}>player</li>;
    });
    return (
      <div>
        <ul>{top_10}</ul>
      </div>
    );
  }
}

export default Topten;
