import React from "react";
import ReactDom from "react-dom";
import axios from "axios";
import {Project} from "./project";

import "./index.css";
import bg from "./Background.png";

import search_icon from "./search.svg";

const BACKGROUND = bg;

class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            projects: {},
            search_query: "",
            search_open: false
        };
        this.search = React.createRef();
    }
    componentDidMount() {
        axios.get('api/get_projects')
            .then((response) => {
                console.log(response.data);
                this.setState({
                    ...this.state,
                    projects: response.data
                })
            });
    }
    onSearchInput() {
        const value = this.search.current.value;
        this.setState({
            ...this.state,
            search_query: value
        });
    }
    searchClick() {
        this.setState({
            ...this.state,
            search_open: !this.state.search_open
        });
    }
    render() {
        const display_projects = [];
        for (let [project_name, description] of Object.entries(this.state.projects)) {
            if(!this.state.search_query || project_name.toLowerCase().includes(this.state.search_query.toLowerCase())) {
                display_projects.push(<Project key={project_name} data_name={project_name} data_description={description}/>);
            }
        }
        return (<div className="Container"
                     draggable="false"
                     style={{
                         backgroundImage: `url(${BACKGROUND})`,
                         backgroundSize: "100% 100%",
                         backgroundRepeat: "no-repeat"

                     }}>
            <div className="MainContent">
                <header>
                    <div className="Spacer"/>
                    <div className="Title">
                        <span>PORFAVOR</span>
                    </div>
                    <div className="Spacer"/>
                    <div className="Search" style={{
                        width: this.state.search_open? "100%" : ""
                    }}>
                        <input ref={this.search}
                               style={{
                                   marginLeft: this.state.search_open? "10px" : ""
                               }}
                               onInput={this.onSearchInput.bind(this)}
                               placeholder="Search" type="text"/>
                        <div className="ImgContainer" onClick={this.searchClick.bind(this)}>
                            <img src={search_icon}/>
                        </div>
                    </div>
                </header>
                <div className="ProjectsContainer">
                    <div className="Projects">
                        {display_projects}
                    </div>
                </div>
                <footer/>
            </div>
        </div>);
    }
}


ReactDom.render(<App/>, document.getElementById("App"));
