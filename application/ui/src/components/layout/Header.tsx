import { Header as NHSHeader } from "nhsuk-react-components";

const Header = (): JSX.Element => {
	return (
		<NHSHeader transactional={true}>
			<NHSHeader.Container>
				<NHSHeader.Logo href="/" />
				<NHSHeader.ServiceName href="/">
					DoS Comparison Tool
				</NHSHeader.ServiceName>
			</NHSHeader.Container>
		</NHSHeader>
	);
};

export default Header;
