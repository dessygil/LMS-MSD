import React from 'react';


export default function Footer() {
  return (
    <footer className="bg-gray-800 text-white px-6 py-4" data-testid="footer">
      <div className="container mx-auto flex flex-wrap items-center justify-between">
        <div>
          <h5 className="text-lg mb-2">Your Business Name</h5>
          <p className="text-sm">123 Street, City, State, Zip</p>
          <p className="text-sm">Email: info@yourbusiness.com</p>
          <p className="text-sm">Phone: (123) 456-7890</p>
        </div>

        <div>
          <h5 className="text-lg mb-2">Links</h5>
          <ul className="space-y-1 text-sm">
            <li><a href="#">Services</a></li>
            <li><a href="#">Research</a></li>
            <li><a href="#">Publications</a></li>
            <li><a href="#">Team</a></li>
            <li><a href="#">Contact Us</a></li>
          </ul>
        </div>

        <div>
          <h5 className="text-lg mb-2">Follow us</h5>
          <div className="flex space-x-2 text-lg">
            <a href="#">facebook icon</a>
            <a href="#">twitter icon</a>
            <a href="#">instagram icon</a>
            <a href="#">linkedin icon</a>
          </div>
        </div>
      </div>

      <div className="mt-4 text-center text-sm border-t border-gray-700 pt-4">
        &copy; {new Date().getFullYear()} Your Business Name. All rights reserved.
      </div>
    </footer>
  );
}
