import React from "react";
import PropTypes from "prop-types";
import key from "weak-key"
const Sidebar = ({data_category}) =>
  !data_category.length ? (
      <li>0 categorías</li>
) : (
  <ul className="sidebar-nav">
    {data_category.map(el =><li key={key(el)}>{el.name}</li>)}
  </ul>
);

Sidebar.propTypes = {
  data_category: PropTypes.array.isRequired
};
export default Sidebar;
