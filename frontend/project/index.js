import React from "react";

import project_icon from "./img/project_icon.png";

import "./project.css";
import {Decore} from "./decore";

const DEFAULT_PROJECT_ICON = project_icon;

export class Project extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            project_name: props.data_name,
            icon_src: props.data_description.icon !== null?
                props.data_description.icon:DEFAULT_PROJECT_ICON,
            decores: [],
            isClicked: false
        };

        this.container = React.createRef();
    }

    get href() {
        return `projects/${this.state.project_name}/index.html`;
    }

    createDecore(e) {
        const container = this.container.current;
        let currentTargetRect = e.currentTarget.getBoundingClientRect();
        const event_offsetX = e.pageX - currentTargetRect.left,
            event_offsetY = e.pageY - currentTargetRect.top;
        const width = container.offsetWidth;
        this.setState({
            ...this.state,
            isClicked: true,
            decores: this.state.decores.concat([<Decore x={event_offsetX} y={event_offsetY} key={this.state.decores.length} width={width}/>])
        });
    }
    resetDecore() {
        this.setState({
            ...this.state,
            isClicked: false,
            decores: this.state.decores.slice(1)
        });
    }
    onMouseUp(e) {
        if(e.button === 0) {
            this.resetDecore();
            window.location = this.href;
        }
    }
    render() {
        const decores = this.state.decores;

        return (
        <div className={`ProjectContainer ${this.state.isClicked? "clicked": ""}`} ref={this.container} onMouseUp={this.onMouseUp.bind(this)}
             onMouseDown={this.createDecore.bind(this)} onMouseLeave={this.resetDecore.bind(this)}>
            <div className="Decore">
                {decores}
            </div>
            <div className="Picture"><img src={this.state.icon_src} draggable="false"/></div>
            <div className="Name"><span>{this.state.project_name}</span></div>
        </div>)
    }
}