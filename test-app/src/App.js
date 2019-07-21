import React from "react";
import Topten from "./components/Top10/Topten";
import PlayerOverview from "./components/PlayerOverview/PlayerOverview";
import "./App.css";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <Topten />
        <PlayerOverview
          title="Player Overview"
          url="/api/player_overview/"
          player="Roger Federer"
        />
        <PlayerOverview
          title="Tournament Overview"
          url="/api/tournament_overview/"
          player="Wimbledon"
        />
        <PlayerOverview
          title="Player Win/Loss"
          url="/api/player_win_loss/"
          player="Roger Federer"
        />
        <PlayerOverview
          title="Player Win/Loss"
          url="/api/player_win_loss/"
          player="Roger Federer"
          url_extra="?tour="
          player_extra="*"
        />
      </header>
    </div>
  );
}

export default App;
