import React from 'react';
import PropTypes from 'prop-types';

import AppBar from '@mui/material/AppBar';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';

function AppToolbar(props) {
  const { openSideMenu } = props;

  return (
    <>
      <AppBar elevation={0}>
        <Toolbar>
          <IconButton
            size="large"
            edge="start"
            color="inherit"
            aria-label="menu"
            sx={{ mr: 2 }}
            onClick={openSideMenu}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" component="div">
            Scroll to elevate App bar
          </Typography>
        </Toolbar>
      </AppBar>
      <Toolbar />
    </>
  );
}

AppToolbar.propTypes = {
  openSideMenu: PropTypes.func.isRequired,
};

export default AppToolbar;
