import React from "react";
import ReactDom from "react-dom";
import axios from "axios";
import {Project} from "./project";

import "./index.css";

class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            projects: {}
        }
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

    render() {
        const display_projects = [];
        for (let [project_name, description] of Object.entries(this.state.projects)) {
            display_projects.push(<Project key={project_name} data_name={project_name} data_description={description}/>);
        }
        return (<div>
            {display_projects}
        </div>);
    }
}


ReactDom.render(<App/>, document.getElementById("App"));
