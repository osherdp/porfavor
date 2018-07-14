import React from "react";

import "./decore.css";
export class Decore extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            width: 0
        };
    }

    componentDidMount() {
        setTimeout(()=>{
            this.setState({
                ...this.state,
                width: this.props.width
            });
        }, 1);
    }
    render() {
        return (<div style={{
            transform: `scale(${this.state.width}, ${this.state.width})`,
            top: this.props.y,
            left: this.props.x
        }} className="DecoreNode"/>)
    }
}