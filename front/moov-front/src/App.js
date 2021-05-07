import React, { useState} from 'react';
import Transport from './components/transport'

function App() {

  const [station, updateStation] = useState("");
  const [searchReq, updateSearchReq] = useState("");
  const [loaded, updateLoaded] = useState(new Set());

  return (
    <div className="App">
      <Transport loaded={loaded} updateLoaded={updateLoaded} station={station} updateStation={updateStation} searchReq={searchReq} updateSearchReq={updateSearchReq}/>
    </div>
  )
}

export default App;
