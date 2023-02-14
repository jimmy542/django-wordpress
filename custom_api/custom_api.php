<?



/**
* Plugin Name: custom rest api 
* Plugin URI: https://github.com/jimmy542
* Description: custom rest api
* Version: 1.0.0
* Author: worawut wattana
* Author URI: https://github.com/jimmy542
* License: GPL2
*/



add_action( 'rest_api_init', 'register_meta_fields');
function register_meta_fields(){

    register_meta( 'post', '_yoast_wpseo_focuskw', array(
        'type' => 'string',
        'description' => '_yoast_wpseo_focuskw',
        'single' => true,
        'show_in_rest' => true
    ));


    register_meta( 'post', '_yoast_wpseo_metadesc', array(
        'type' => 'string',
        'description' => '_yoast_wpseo_metadesc',
        'single' => true,
        'show_in_rest' => true
    ));

}

?>