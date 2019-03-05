import React from "react";
import PropTypes from "prop-types";
import key from "weak-key";

/* function deleteClick(id){

   var url = "/api-scraper/";
   var xhr = new XMLHttpRequest();
   xhr.open("DELETE", url+'', true);
   xhr.load = function () {
	 var books = JSON.parse(xhr.responseText);
	 if (xhr.readyState == 4 && xhr.status == "200") {
		  console.table(books);
	 } else {
		   console.error(books);
	 }
  }
  xhr.send(null);
  return;
} */

const Table = ({ data }) =>
  !data.length ? (
    <p>Aún no hay datos. Para empezar el scrapping, presione el botón en la esquina superior derecha.</p>
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
              <td>{el.price} £ </td> <td>{el.stock}  </td>
              <td> {el.description} </td> <td> {el.UPC} </td> <td> {el.category} </td>
              /*<td id="delete_book">  <button onclick={delete(el.id)}> Borrar </button></td>*/
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
