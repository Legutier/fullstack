import React, { Component } from "react";
import PropTypes from "prop-types";
class DataProvider extends Component {

  state = {
      data: [],
      loaded: false,
      placeholder: "Loading..."
    };
  componentDidMount() {
    fetch('api-scraper')
      .then(response => {
        if (response.status !== 200) {
          return this.setState({ placeholder: "Something went wrong" });
        }
        return response.json();
      })
      .then(data => this.setState({ data: data, loaded: true }));
  }
  render() {
    const { data, loaded, placeholder } = this.state;
    return (loaded ? ({this.state.data.map(el => (
      <tr key={el.id}>
        <td>{el.title}</td> <td> <img src={el.thumbnail}/> </td>
        <td>{el.price} £ </td> <td>{el.stock}  </td>
        <td> {el.description} </td> <td> {el.UPC} </td> <td> {el.category} </td>
        <td id="delete_book"> delete </td>))}) : (<p>{placeholder}</p>);)
  }
}
export default DataProvider;
