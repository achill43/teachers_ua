import React from 'react';
import { Link } from "react-router-dom";
import styles from './Sidebar.module.scss';

const SideBar: React.FC = () => {
    return (
        <div className={styles.sidebar}>
            <h2 className={styles.text_center}><span className={styles.underscore}>Tutor UA</span></h2>
            <div className="menu">
                <Link to="/" className={styles.menu_item}>Home</Link>
                <Link to="/login" className={styles.menu_item}>Sign In</Link>
                <Link to="/login" className={styles.menu_item}>Sign Up</Link>
                <Link to="/about" className={styles.menu_item}>About Us</Link>
            </div>
        </div>
    );
};

export default SideBar;