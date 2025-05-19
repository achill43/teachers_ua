import React, { useState } from "react";
import { Link } from "react-router-dom";
import { useDispatch } from "react-redux";
import styles from './SignIn.module.scss';
import { setAuthData } from "../store/authSlice";
import api from "../api/axios";




interface FormData {
  email: string;
  password: string;
}


const SignIn: React.FC = () => {
  const dispatch = useDispatch();
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
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    console.log("Form submitted:", formData);
    const response = await api.post("/users/sign_in/", formData).then((response) => {
        const { user, session } = response.data;
        dispatch(setAuthData({ user, session }));
        console.log("✅ You are SingIn:", response.data);
    })
    .catch((error) => {
        if (error.response) {
        console.error("❌ Server error:", error.response.data);
        }
    });
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
                  <button className="btn">Sign In</button>
                  <Link to="/sign_up" className="btn btn-dark">Sign Up</Link>
              </div>
          </form>
        </div>
    </div>
  );
};

export default SignIn;