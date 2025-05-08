import React from "react";
import { Link } from "react-router-dom";

const Login: React.FC = () => {
  return (
    <div>
        
            <h1>Login page </h1>
            <Link to="/about">Go to About </Link>
    </div>
  );
};

export default Login;