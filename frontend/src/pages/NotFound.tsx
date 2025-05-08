import React from "react";
import { Link } from "react-router-dom";

const Home: React.FC = () => {
  return (
    <div>
            <h1>Page not exist!</h1>
            <p>Such page not exiist! <Link to="/">Go to Home page </Link></p>
    </div>
  );
};

export default Home;