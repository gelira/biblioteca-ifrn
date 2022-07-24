import React from 'react';
import PropTypes from 'prop-types';

import Drawer from '@mui/material/Drawer';

function SideMenu(props) {
  const {
    sideMenuIsOpen,
    closeSideMenu,
  } = props;

  return (
    <Drawer
      anchor="left"
      open={sideMenuIsOpen}
      onClose={closeSideMenu}
    >
      TESTE
    </Drawer>
  );
}

SideMenu.propTypes = {
  sideMenuIsOpen: PropTypes.bool.isRequired,
  closeSideMenu: PropTypes.func.isRequired,
};

export default SideMenu;
