import React from "react";


import "./tabs.css";
import {Tab} from "./tab";

export class Tabs extends React.Component {
    constructor(props) {
        super(props);
        this.all_tab = React.createRef();
        this.tabs = [
            <Tab key="all" name="All Projects" ref={this.all_tab}/>,
        ];
    }
    componentDidMount() {
        this.all_tab.current.select();
    }
    get app() {
        return this.props.app;
    }

    render() {
        return (
        <div className="Tabs">
            {this.tabs}
        </div>
        );
    }
}