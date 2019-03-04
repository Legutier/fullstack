import React from "react";
import PropTypes from "prop-types";
import key from "weak-key";

handleClick = userId => {
  const requestOptions = {
    method: 'DELETE'
  };

const Table = ({ data }) =>
  !data.length ? (
    <p>Nothing to show</p>
  ) : (
    <div className="column">
      <h2 className="subtitle">
        Showing <strong>{data.length} items</strong>
      </h2>
      <table className="table is-striped">
        <thead>
          <tr>
            <th>Título </th> <th> Imagen </th> <th> Precio </th>
            <th> Stock </th> <th> Descripción </th>
            <th> UPC </th> <th> Categoría </th>
          </tr>
        </thead>
        <tbody>
          {data.map(el => (
            <tr key={el.id}>
              <td>{el.title}</td> <td> <img src={el.thumbnail}/> </td>
              <td>{el.price}</td> <td>{el.stock}  </td>
              <td> {el.description} </td> <td> {el.UPC} </td> <td> {el.category} </td>
           </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
Table.propTypes = {
  data: PropTypes.array.isRequired
};
export default Table;
