import React, { useState } from "react";
import styles from './Login.module.scss';

interface FormData {
  email: string;
  password: string;
}


const Login: React.FC = () => {
    const [formData, setFormData] = useState({
      email: "",
      password: "",
  });

  const handleChange = (e: React.ChangeEvent) => {
      const { name, value } = e.target;

      setFormData((prev) => ({
      ...prev,
      [name]: value,
      }));
  };
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log("Form submitted:", formData);
  };


  return (
    <div>
          <div className={styles.card}>
            <form className={styles.myForm} onSubmit={handleSubmit}>
              <h1 className="text-center"><span className="underscore">Sign In</span></h1>
              <div className={styles.row}>
                  <div className={styles.col30}>
                      Email: 
                  </div>
                  <div className={styles.col70}>
                      <input 
                          type="email" name="email" placeholder="Enter email" 
                          className="form-control" value={formData.email} onChange={handleChange}/>
                  </div>
              </div>
              <div className={styles.row}>
                  <div className={styles.col30}>
                      Password: 
                  </div>
                  <div className={styles.col70}>
                      <input 
                          type="password" name="password" placeholder="Enter password"
                          className="form-control" value={formData.password} onChange={handleChange}/>
                  </div>
              </div>
              <div className={styles.row}>
                  <button className="btn">Login</button>
                  <button className="btn btn-dark">Registration</button>
              </div>
          </form>
        </div>
    </div>
  );
};

export default Login;