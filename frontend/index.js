import React from "react";
import ReactDom from "react-dom";
import axios from "axios";
import {Project} from "./project";

import "./index.css";

import search_icon from "./search.svg";
import {Tabs} from "./tabs/index";

class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            projects: {},
            search_query: ""
        };
        this.search = React.createRef();
    }
    componentDidMount() {
        console.log("loading projects");
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
    render() {
        const display_projects = [];
        for (let [project_name, description] of Object.entries(this.state.projects)) {
            if(!this.state.search_query || project_name.toLowerCase().includes(this.state.search_query.toLowerCase())) {
                display_projects.push(<Project key={project_name} data_name={project_name} data_description={description}/>);
            }
        }
        return (<div className="Container">
            <h1>PorFavor</h1>
            <h4>Publishing static documentation the easiest way possible!</h4>
            <div className="TopBar">
                <Tabs app={this}/>
                <div className="Spacer"/>
                <div className="Search"><img src={search_icon}/><input ref={this.search}
                                                                       onInput={this.onSearchInput.bind(this)}
                                                                       placeholder="Search" type="text"/></div>
            </div>
            <hr/>
            <div className="Projects">
                {display_projects}
            </div>
        </div>);
    }
}


ReactDom.render(<App/>, document.getElementById("App"));
