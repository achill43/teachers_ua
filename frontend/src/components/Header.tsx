import React from 'react';
import { Link } from "react-router-dom";
import styles from './Header.module.scss';

const Header: React.FC = () => {
    return (
        <nav className={styles.mainMenu} id="mainMenu">
            {/* <button className={[styles.Hamburger, styles.cHamburgerLine].join(' ')} id="showMenu">
            <span></span>
            </button> */}
                
            <ul className={styles.myMenu}>
                <li className={styles.menuItem}>
                    <Link to="/" className={styles.menu_item}>Home</Link>
                </li>
                <li>
                    <Link to="/sign_in" className={styles.menu_item}>Sign In</Link>
                </li>
                <li>
                    <Link to="/about" className={styles.menu_item}>About Us</Link>
                </li>
                <li>
                    <form name="searchForm" action="{% url 'search' %}" method="get" className="form-inline form-search">
                        <div className="input-goup">
                            <i className="glyphicon glyphicon-search"></i>
                            <i className="glyphicon glyphicon-triangle-bottom"></i>
                            <input className="form-control" id="searchInput" type="text" name="search" placeholder="search"/>
                        </div>
                    </form>
                </li>
            </ul>
        </nav>
    );
};

export default Header;