import React, { useState } from "react";
import styles from './Login.module.scss';

enum Role {
    teacher = "Teacher",
    student = "Student"
}

interface FormData {
    first_name: string;
    last_name: string;
    email: string;
    password: string;
    r_password: string;
    role: Role;
}

interface FormErrors {
    first_name: string;
    last_name: string;
    email: string;
    password: string;
    r_password: string;
    role: string;
}


const SignUp: React.FC = () => {
    const [formData, setFormData] = useState({
        first_name: "",
        last_name: "",
        email: "",
        password: "",
        r_password: "",
        role: Role.student,
    });
    const [FormErrors, setFormErrors] = useState({
        first_name: "",
        last_name: "",
        email: "",
        password: "",
        r_password: "",
        role: "",
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
        if (formData.password != formData.r_password) {
            setFormErrors((prev) => ({
                ...prev,
                ["password"]: "Password and Confirm must be the same!",
            }));
        }
    };


    return (
        <div>
            <div className={styles.card}>
                <form className={styles.myForm} onSubmit={handleSubmit}>
                <h1 className="text-center"><span className="underscore">Sign Up</span></h1>
                <div className={styles.row}>
                    <div className={styles.col30}>
                        First Name: 
                    </div>
                    <div className={styles.col70}>
                        <input 
                            type="text" name="first_name" placeholder="Enter your First name" 
                            className="form-control" value={formData.first_name} onChange={handleChange}/>
                    </div>
                </div>
                <div className={styles.row}>
                    <div className={styles.col30}>
                        Last Name: 
                    </div>
                    <div className={styles.col70}>
                        <input 
                            type="text" name="last_name" placeholder="Enter your Last name" 
                            className="form-control" value={formData.last_name} onChange={handleChange}/>
                    </div>
                </div>
                <div className={styles.row}>
                    <div className={styles.col30}>
                        Email: 
                    </div>
                    <div className={styles.col70}>
                        <input 
                            type="email" name="email" placeholder="Enter your email" 
                            className="form-control" value={formData.email} onChange={handleChange}/>
                    </div>
                </div>

                {FormErrors.email && (
                    <div className={`${styles.row} ${styles.errorBlock}`}>
                        {FormErrors.email}
                    </div>
                )}

                <div className={styles.row}>
                    <div className={styles.col30}>
                        Password: 
                    </div>
                    <div className={styles.col70}>
                        <input 
                            type="password" name="password" placeholder="Enter your password"
                            className="form-control" value={formData.password} onChange={handleChange}/>
                    </div>
                </div>
                <div className={styles.row}>
                    <div className={styles.col30}>
                        Confirm password: 
                    </div>
                    <div className={styles.col70}>
                        <input 
                            type="password" name="r_password" placeholder="Enter password again"
                            className="form-control" value={formData.r_password} onChange={handleChange}/>
                    </div>
                </div>

                {FormErrors.password && (
                    <div className={`${styles.row} ${styles.errorBlock}`}>
                        {FormErrors.password}
                    </div>
                )}

                <div className={styles.row}>
                    <div className={styles.col30}>
                        Role: 
                    </div>
                    <div className={styles.col70}>
                    <select 
                        name="role" 
                        className="form-control" 
                        value={formData.role} 
                        onChange={handleChange}
                    >
                        {Object.values(Role).map((role) => (
                            <option key={role} value={role}>{role}</option>
                        ))}
                    </select>
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

export default SignUp;