import {useState, useEffect} from 'react';
import axios from "axios";
import Article_card from './components/Article_card';
import Overview from './components/Overview';
import './App.css';
const App = () => {

  const [articles, set_articles] = useState([]);
  const [offset, update_offset] = useState(30)
  const [overview_data, update_overview_data] = useState({})
  const FetchArticles = async(offset, limit) => {
    try{
      let response = await axios.get(`http://localhost:8000/fetch_articles/${offset}/${limit}`);
      return response
    } catch (error){
      console.log(error);
    }
  };

  const FetchAnalyticData = async() => {
    try{
      let response = await axios.get('http://localhost:8000/fetch_analytic_data');
      let data = {
        'total': response.data.total, 
        'critical': response.data.critical, 
        'high': response.data.high, 
        'medium': response.data.medium,
        'low': response.data.low
      }
      update_overview_data(data)
    } catch (error){
      console.log(error)
    }
  }

  const ViewMore = async (offset) => {
    let new_articles = await FetchArticles(offset,30)
    let article_array = new_articles.data
    update_offset(offset += 30)
    set_articles([...articles, ...article_array])
  }

  
  useEffect(() => { 
    const InitialFetch = async() => {
    let new_articles = await FetchArticles(0,30)
    let article_array = new_articles.data
    set_articles([...article_array])
    }
    InitialFetch()
    FetchAnalyticData()
  },[])

  return (
  <>
    {overview_data != null ? <Overview total={overview_data.total} critical={overview_data.critical} high={overview_data.high} medium={overview_data.medium} low={overview_data.low}/>: <div></div> }
    <div className='feedRow'>
        {articles.length > 0 ? articles.map((article, i) => (
          <div className="feedItem">
            <Article_card 
              date = {article.date}
              description={article.description}
              link = {article.link}
              publisher = {article.publisher}
              severity = {article.severity}
              tags = {article.tags}
              title = {article.title}
              key = {i}
            />
          </div>
        )) : <div></div>}
    </div>
    <div className="addRow">
        <button onClick={() => {ViewMore(offset)}}>See More Articles</button>
    </div>
  </>
  );
};

export default App