import React from 'react';

import Box from '@mui/material/Box';
import Container from '@mui/material/Container';

import AppToolbar from '../components/AppToolbar';
import SideMenu from '../components/SideMenu';

function Main() {
  const [sideMenuIsOpen, setSideMenuIsOpen] = React.useState(false);

  const openSideMenu = () => setSideMenuIsOpen(true);
  const closeSideMenu = () => setSideMenuIsOpen(false);

  return (
    <>
      <AppToolbar openSideMenu={openSideMenu} />
      <SideMenu sideMenuIsOpen={sideMenuIsOpen} closeSideMenu={closeSideMenu} />
      
      <Container>
        <Box sx={{ my: 2 }}>
          {[...new Array(12)]
            .map(
              () => `Cras mattis consectetur purus sit amet fermentum.
Cras justo odio, dapibus ac facilisis in, egestas eget quam.
Morbi leo risus, porta ac consectetur ac, vestibulum at eros.
Praesent commodo cursus magna, vel scelerisque nisl consectetur et.`,
            )
            .join('\n')}
        </Box>
      </Container>
    </>
  );
}

export default Main;
