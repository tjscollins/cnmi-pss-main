<?php
/**
 * Template part for displaying results in search pages
 *
 * @link https://codex.wordpress.org/Template_Hierarchy
 *
 * @package CNMI_PSS
 */

?>

<article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
    <div class="row">
    <header class="search-entry-header col-xs-12">
        <?php
	$name = get_the_title();
	$title = get_field('job_title');
	if (strlen($title) > 0) {
	    $name .= ' - ' . $title;
	}
	$post_type = get_post_type();
	if ($post_type == 'post') {
	    $post_type = 'News';
	}
	$post_type = preg_replace('/\_/', ' ', $post_type);
	$post_type = ucwords($post_type);
	echo '<h2 class="search-entry-title">' .
             '<span class="screen-reader-text">Search Result: '. $post_type . ' ' . $name . '</span>' .
	     '<span aria-hidden="true">' . $post_type . ':</span> </h2>' .
	     '<a href="' .
	     esc_url(get_permalink()) .
	     '" rel="bookmark">' .
	     $name .
	     '</a>'; ?>

        <?php if ( 'post' === get_post_type() ) : ?>
            <div class="search-entry-meta">
                <p>&nbsp; <?php echo get_the_date(); ?></p>
            </div>
            <!-- .entry-meta -->
        <?php endif; ?>
    </header>
    <!-- .entry-header -->

    <div class="search-entry-summary col-xs-12 col-sm-10 col-sm-push-1">
        <?php the_excerpt(); ?>
    </div>
    <!-- .entry-summary -->

    <footer class="entry-footer col-xs-12">
        <?php cnmi_pss_entry_footer(); ?>
    </footer>
    <!-- .entry-footer -->
    </div>
    <hr />
</article>
<!-- #post-<?php the_ID(); ?> -->
