import React, { useState } from "react";
import { RenderJSON } from "../../RenderJSON";
import axios from "axios";

async function getPlayerOverview(player, url, extra, player_extra) {
  // const url = "/api/player_overview/";
  let final_url;
  if (extra !== undefined && extra !== null) {
    final_url = url + player + extra + player_extra;
  } else {
    final_url = url + player;
  }
  return await axios.get(final_url);
}

function PlayerOverviewHidden(props) {
  let player_name = props.player_name || "Roger Federer";

  let play_overview;
  const [textedJSON, setTextedJSON] = useState(null);
  play_overview = getPlayerOverview(
    player_name,
    props.url,
    props.url_extra,
    props.player_extra_new
  );

  play_overview.then(p_o => {
    setTextedJSON(JSON.stringify(p_o.data, undefined, 4));
  });

  if (textedJSON === null) {
    return <div>Loading...</div>;
  } else {
    const commonProps = {
      fontSize: "18px",
      json_text: textedJSON,
      rows: 20,
      cols: 80,
      ...props
    };
    return (
      <div>
        <RenderJSON {...commonProps} />
      </div>
    );
  }
}

const PlayerOverview = props => {
  const [playerName, setPlayerName] = useState(props.player);
  const [player_extraName, setPlayerExtraName] = useState(props.player_extra);

  function handleChange(e) {
    e.preventDefault();
    setPlayerName(e.target.value || props.player);
  }
  function handleChange_query(e) {
    e.preventDefault();
    setPlayerExtraName(e.target.value || props.player_extra);
  }

  const modProps = {
    extra: (
      <span className="inputHolder">
        {props.url}
        <input onChange={handleChange} placeholder={props.player} />
      </span>
    ),
    extra_query: (
      <span className="inputHolder">
        {props.url_extra ? props.url_extra : ""}
        {props.player_extra ? (
          <input
            onChange={handleChange_query}
            placeholder={props.player_extra}
          />
        ) : (
          ""
        )}
      </span>
    ),
    player_name: playerName,
    player_extra_new: player_extraName,
    url: props.url,
    ...props
  };
  return (
    <div>
      <PlayerOverviewHidden {...modProps} />
    </div>
  );
};

export default PlayerOverview;
