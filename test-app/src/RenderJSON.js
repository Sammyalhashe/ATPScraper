import React from "react";
import "./RenderJSON.css";

function RenderJSON(props) {
  const divStyle = {
    fontSize: props.fontSize || "23px"
  };
  let json_text;
  if (props.json_text === '""') {
    json_text = <div />;
  } else {
    json_text = (
      <div>
        <textarea
          wrap="off"
          readOnly
          rows={props.rows || 20}
          cols={props.cols || 30}
          style={divStyle}
          value={props.json_text}
          className="top-10"
        />
      </div>
    );
  }
  return (
    <div className="holder">
      <div className="title">{props.title}</div>
      {props.extra}
      {props.extra_query}
      {json_text}
    </div>
  );
}

export { RenderJSON };
