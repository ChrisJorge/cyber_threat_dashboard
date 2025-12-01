import '../styling/Nav_bar.css'
const Nav_bar = () => {
  return (
    <div className="navBarContainer">
        <div className="navigationOptionContainer">
            <p className="optionText">Insights</p>
        </div>
        <div className="navigationOptionContainer">
            <p className="optionText">Feed</p>
        </div>
        <div className="navigationOptionContainer">
            <p className="optionText">Profile</p>
        </div>
    </div>
  )
}

export default Nav_bar