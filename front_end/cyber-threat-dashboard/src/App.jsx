import {useState, useEffect} from 'react';
import axios from "axios";
import Article_card from './components/Article_card';
import './App.css';
const App = () => {

  const [articles, set_articles] = useState([]);

  const FetchArticles = async(offset, limit) => {
    try{
      let response = await axios.get(`http://localhost:8000/fetch_articles/${offset}/${limit}`);
      return response
    } catch (error){
      console.log(error);
    }
  };

  useEffect(() => {
    const InitialFetch = async() => {
      let new_articles = await FetchArticles(0,30)
      let article_array = new_articles.data
      set_articles([...article_array])
    }
    InitialFetch()
  },[])

  return (
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
  );
};

export default App