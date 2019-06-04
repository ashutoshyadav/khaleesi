import React, { useState, useEffect } from 'react';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import Select from '@material-ui/core/Select';
import MenuItem from '@material-ui/core/MenuItem';
import Pie3D from 'react-pie3d'
import './App.css';

function fetchData(dataSetter){
  console.log('calling api');
  fetch('http://127.0.0.1:5000/portfolio').then(response => {
    response.json().then( values => {
      console.log('got the data')
      dataSetter(values)
    })
  })
}

function getData(data, amount, riskAppetite){
  console.log(data);
  console.log(amount);
  console.log(riskAppetite)
  const res = Object.keys(data).map(key => {
    let val = data[key][riskAppetite] * amount
    console.log(data[key][riskAppetite])
    console.log(val);
    return {
      value: val,
      label: key
    }
  })
  console.log(res)
  return res
}


function App() {
  const [amount, setAmount] = useState(10000);
  const [riskAppetite, setRiskAppetite] = useState('averse');
  const [data, setData] = useState(null);
  const [result, setResultState] = useState(false);

  console.log(riskAppetite)

  useEffect(() => {
    data === null && fetchData(setData, []);
  }, [data])

  return (
    <div className="App">
      <header className="App-header">
        <p style={{margin:`30px`}}>
          I want to invest amount of 
          $<TextField 
            style={{
              color: 'white',
              marginLeft: `20px`,
              marginRight: `20px`
            }}
            value={amount}
            onChange={e => setAmount(e.target.value)}
          /> with risk profile 
          <Select
            value={riskAppetite}
            onChange={e => setRiskAppetite(e.target.value)}
            style={{
              color: 'white',
              marginLeft: `20px`,
              marginRight: `20px`
            }}
            inputProps={{
              name: 'age',
              id: 'age-simple',
            }}
          > 
            <MenuItem value={'averse'}>Averse</MenuItem>
            <MenuItem value={'moderate'}>Moderate</MenuItem>
            <MenuItem value={'aggressive'}>Aggressive</MenuItem>
          </Select>
        </p>

        <Button 
          variant="contained" 
          color="primary" 
          onClick={e => {
            setResultState(true);
          }}
        >
          Submit
        </Button>

        {result && <Pie3D data={getData(data, amount, riskAppetite)} style={{color:'white'}} /> }

      </header>
    </div>
  );
}

export default App;
