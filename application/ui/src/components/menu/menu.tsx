import React from "react";
import { MENU_PAGE } from "../../constants/componentIds";
import Layout from "../common/Layout";
import MenuCards from "./menuCards";

export default class Menu extends React.Component {
	render(): React.JSX.Element {
		return (
			<Layout>
				<div id={MENU_PAGE}>
					<h1> Select a Search </h1>
					<p> Select a search to compare </p>
				</div>
				<MenuCards />
			</Layout>
		);
	}
}
