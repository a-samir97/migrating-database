import React from 'react';
import Config  from './components/config'
import  { Table }   from './components/Tables'
import { Route, Switch } from 'react-router-dom'

function App() {
  return (
    <Switch>
      <Route path="/" component={ Config } exact></Route>
      <Route path='/tables' component={ Table } exact></Route>
    </Switch>
  );
}

export default App;
