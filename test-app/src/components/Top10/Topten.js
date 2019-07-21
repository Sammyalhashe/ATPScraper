import React, { Component } from "react";
import {RenderJSON} from "../../RenderJSON"
import axios from "axios";
import "./Topten.css";

class Topten extends Component {
  constructor(props) {
    super(props);
    this.state = {
      data: ''
    };
  }
  componentDidMount() {
    this.getData();
  }

  getData = () => {
    axios.get("/api/top_10").then(response => {
      this.setState({ data: response.data });
    });
  };
  render() {
	  const textedJSON = JSON.stringify(this.state.data, undefined, 4);
	  // let json_text;
	  // if (Object.entries(this.state.data).length === 0 && this.state.data.constructor === Object) {
		  // json_text = <div></div>;
	  // } else {
		  // json_text = <div><textarea rows="20" cols="30" defaultValue={textedJSON} className="top-10"></textarea></div>;
	  // }
	  
    return (
      <div>
		  <RenderJSON title="Top Ten" json_text={textedJSON} />
      </div>
    );
  }
}

export default Topten;
