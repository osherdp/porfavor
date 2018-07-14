import React from "react";

import "./tab.css";


const SELECTED_COLOR = "#1976D2";
const HOVERED_COLOR = "#9E9E9E";
const UNSELECTED_COLOR = "";

export class Tab extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            selected: false,
            hovered: false
        };
    }
    select() {
        this.setState({
            ...this.state,
            selected: true
        });
    }
    onMouseOver() {
        this.setState({
            ...this.state,
            hovered: true
        });
    }
    onMouseLeave() {
        this.setState({
            ...this.state,
            hovered: false
        });
    }
    get decoreColor() {
        if (this.state.selected) {
            return SELECTED_COLOR;
        }
        else if(this.state.hovered) {
            return HOVERED_COLOR;
        }
        return UNSELECTED_COLOR;
    }
    render() {
        return (
        <div className="Tab" onMouseOver={this.onMouseOver.bind(this)} onMouseLeave={this.onMouseLeave.bind(this)}>
            <div className="Name">{this.props.name}</div>
            <div className="Decore" style={{backgroundColor: this.decoreColor}}/>
        </div>
        );
    }
}