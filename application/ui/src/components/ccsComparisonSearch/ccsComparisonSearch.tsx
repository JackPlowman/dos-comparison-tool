import { Button, Container, Form, Pagination } from "nhsuk-react-components";
import React from "react";
import { useNavigate } from "react-router-dom";
import { useAppDispatch, useAppSelector } from "../../app/hooks";
import {
	AGE_INPUT_SUFFIX,
	AGE_UNITS_DROP_DOWN_SUFFIX,
	CCS_COMPARISON_SEARCH_PAGE,
	DISPOSITION_DROP_DOWN,
	ENVIRONMENT_DROP_DOWN_SUFFIX,
	POSTCODE_INPUT,
	PREVIOUS_BUTTON,
	ROLE_DROP_DOWN_SUFFIX,
	SEARCH_BUTTON,
	SEX_DROP_DOWN,
	SYMPTOM_DISCRIMINATOR_DROP_DOWN,
	SYMPTOM_GROUP_DROP_DOWN,
} from "../../constants/componentIds";
import { SEARCH_ONE, SEARCH_TWO } from "../../constants/constants";
import { CCS_COMPARISON_RESULTS_PATH, MENU_PATH } from "../../constants/paths";
import { CCSSearchData } from "../../interfaces/dtos";
import { selectToken } from "../../slices/authSlice";
import { search } from "../../slices/ccsComparisonSearchSlice";
import { Layout } from "../common";
import EnvironmentSearchForm from "./environmentSearchForm";
import SharedSearchForm from "./sharedSearchForm";

/**
 * The CCS comparison search component.
 * @returns A CCS comparison search component.
 */
export default function CCSComparisonSearch() {
	const dispatch = useAppDispatch();
	const idToken = useAppSelector(selectToken) as string;
	const navigate = useNavigate();

	const handleSearchForm = async (event: React.FormEvent<HTMLFormElement>) => {
		/**
		 * Gets the value of an input element.
		 * @param inputName The name of the input element.
		 * @returns The value of the input element.
		 */
		function getElementById(inputName: string) {
			return (document.getElementById(inputName) as HTMLInputElement).value;
		}
		event.preventDefault();
		navigate(CCS_COMPARISON_RESULTS_PATH);

		const postcodeInput = getElementById(POSTCODE_INPUT);
		const disposition = getElementById(DISPOSITION_DROP_DOWN);
		const symptomGroup = getElementById(SYMPTOM_GROUP_DROP_DOWN);
		const symptomDiscriminator = getElementById(
			SYMPTOM_DISCRIMINATOR_DROP_DOWN
		);
		const sex = getElementById(SEX_DROP_DOWN);

		const searchOneEnvironment = getElementById(
			`${SEARCH_ONE}${ENVIRONMENT_DROP_DOWN_SUFFIX}`
		);
		const searchOneAge = getElementById(`${SEARCH_ONE}${AGE_INPUT_SUFFIX}`);
		const searchOneAgeFormat = getElementById(
			`${SEARCH_ONE}${AGE_UNITS_DROP_DOWN_SUFFIX}`
		);
		const searchOneRole = getElementById(
			`${SEARCH_ONE}${ROLE_DROP_DOWN_SUFFIX}`
		);

		const searchTwoEnvironment = getElementById(
			`${SEARCH_TWO}${ENVIRONMENT_DROP_DOWN_SUFFIX}`
		);
		const searchTwoAge = getElementById(`${SEARCH_TWO}${AGE_INPUT_SUFFIX}`);
		const searchTwoAgeFormat = getElementById(
			`${SEARCH_TWO}${AGE_UNITS_DROP_DOWN_SUFFIX}`
		);
		const searchTwoRole = getElementById(
			`${SEARCH_ONE}${ROLE_DROP_DOWN_SUFFIX}`
		);

		const searchData: CCSSearchData = {
			authToken: idToken,
			search_one: {
				age: parseInt(searchOneAge),
				age_format: searchOneAgeFormat,
				disposition: parseInt(disposition),
				gender: sex,
				role: searchOneRole,
				postcode: postcodeInput,
				search_environment: searchOneEnvironment,
				symptom_discriminator_list: [parseInt(symptomDiscriminator)],
				symptom_group: parseInt(symptomGroup),
				search_date_time: "2024-01-31T10:00:00+00:00",
			},
			search_two: {
				age: parseInt(searchTwoAge),
				age_format: searchTwoAgeFormat,
				disposition: parseInt(disposition),
				gender: sex,
				role: searchTwoRole,
				postcode: postcodeInput,
				search_environment: searchTwoEnvironment,
				symptom_discriminator_list: [parseInt(symptomDiscriminator)],
				symptom_group: parseInt(symptomGroup),
				search_date_time: "2024-01-31T10:00:00+00:00",
			},
		};
		await dispatch(search(searchData));
	};

	return (
		<Layout>
			<Container id={CCS_COMPARISON_SEARCH_PAGE}>
				<div>
					<h1>CCS Comparison Search</h1>
					<p>Make a search to compare results from multiple environments</p>
				</div>
				<Form role="form" onSubmit={handleSearchForm}>
					<h2>Search Details</h2>
					<SharedSearchForm />
					<h2>Search 1 Details</h2>
					<EnvironmentSearchForm searchName={SEARCH_ONE} />
					<h2>Search 2 Details</h2>
					<EnvironmentSearchForm searchName={SEARCH_TWO} />
					<br />
					<Button id={SEARCH_BUTTON}>{"Search"}</Button>
					<Pagination id={PREVIOUS_BUTTON}>
						<Pagination.Link
							previous
							onClick={() => {
								navigate(MENU_PATH, { replace: true });
							}}
						>
							Menu Page
						</Pagination.Link>
					</Pagination>
				</Form>
			</Container>
		</Layout>
	);
}
