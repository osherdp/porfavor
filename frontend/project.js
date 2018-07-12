import React from "react";

import project_icon from "./img/project_icon.png";

import "./project.css";

const DEFAULT_PROJECT_ICON = project_icon;

export class Project extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            project_name: props.data_name,
            icon_src: DEFAULT_PROJECT_ICON
        }
    }

    render() {
        return (<a href={`projects/${this.state.project_name}/index.html`}><div className="ProjectContainer">
            <div className="Picture"><img src={this.state.icon_src}/></div>
            <div className="Name"><span>{this.state.project_name}</span></div>
        </div></a>)
    }
}