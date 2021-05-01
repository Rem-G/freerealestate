import React, { useState} from 'react';
import Transport from './components/transport'

function App() {

  const [station, updateStation] = useState("");
  const [searchReq, updateSearchReq] = useState("");
  return (
    <div className="App">
      <Transport station={station} updateStation={updateStation} searchReq={searchReq} updateSearchReq={updateSearchReq}/>
    </div>
  )
}

export default App;
