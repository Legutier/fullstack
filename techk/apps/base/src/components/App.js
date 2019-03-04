import React from "react";
import ReactDOM from "react-dom";
import DataProvider from "./DataProvider";
import Table from "./Table";
import Sidebar from "./Sidebar"

const App = () => (
  <DataProvider endpoint="api-scraper/"
                render={data => <Table data={data} />} />
);


const Sidebar_app = () => (
  <DataProvider endpoint ="api-category/"
                render ={data_category => <Sidebar data_category={data_category} />} />
)


const wrapper = document.getElementById("app");
const wrapperside = document.getElementById("sidebar-wrapper");
wrapper ? ReactDOM.render(<App />, wrapper) : null;
wrapperside ? ReactDOM.render(<Sidebar_app />, wrapperside): null;
