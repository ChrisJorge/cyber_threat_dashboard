import {HashRouter as Router, Routes, Route} from 'react-router-dom';
import Feed_page from './pages/Feed_page';
import './App.css';
const App = () => {
  return(
    <Router>
      <Routes>
        <Route path='/' element={<Feed_page/>}/>
      </Routes>
    </Router>
  )
};

export default App